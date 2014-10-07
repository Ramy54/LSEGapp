package com.ftse.puppet;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.Reader;
import java.sql.SQLException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.apache.log4j.Logger;
import org.yaml.snakeyaml.TypeDescription;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.Constructor;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ftse.puppet.domain.Deployment;
import com.ftse.puppet.domain.Host;
import com.ftse.puppet.domain.Release;
import com.ftse.puppet.rubydto.Metric;
import com.ftse.puppet.rubydto.PuppetLog;
import com.ftse.puppet.rubydto.Report;
import com.ftse.puppet.rubydto.ResourceStatus;
import com.ftse.puppet.rubydto.TransactionEvent;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.DaoManager;
import com.j256.ormlite.support.ConnectionSource;

@SuppressWarnings("serial")
public class PuppetReportCollector extends HttpServlet {

	private static final Logger logger = Logger.getLogger(PuppetReportCollector.class);
	private ConnectionSource connectionSource; 

	public PuppetReportCollector(ConnectionSource connectionSource) {
		this.connectionSource = connectionSource;
	}

	@Override
	/**
	 * This is to be called by a puppet master. It needs to be configured to post it's YAML reports
	 * to this servlet after each puppet run.
	 * This will then go off and fetch all the facts for the run from puppetDB and store this information
	 * in a local database. 
	 */
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		if(!req.getContentType().equals("application/x-yaml")){
			resp.getWriter().append("POST data needs to be of YAML Content Type");
			resp.setStatus(500);
			return;
		}
		
		//Load the Puppet report YAML into the POJOs. 
		Report report = getReportFromYaml(req.getReader());
		
		//Retrieve this host's facts from puppetDB.
		JsonNode facts = getFactsFromPuppetDB(report.host);
		
		if(facts == null){
			logger.error("Found no facts in PuppetDB for host " + report.host);
			resp.setStatus(500);
			return;
		}
		
		//Determine if we're in noop mode. If so, don't do anything as the facts aren't applicable.
		if(report.status.equals("unchanged")){
			logger.info("Noop run detected for " + facts.get("hostname").asText() + ". Ignoring.");
			return;
		}
		if(report.status.equals("failed")){
			logger.info("Failed run detected for " + facts.get("hostname").asText() + ". Ignoring.");
			return;
		}
		
		JsonNode currentPathNode = facts.get("ftse_current_path");
		String installPath = currentPathNode == null ? "Unknown" : currentPathNode.asText();
		
		logger.info("Received release info from Host " + facts.get("hostname").asText() + 
				" with release " + facts.get("ftse_current_release").asText() + 
				" installed at " + installPath);
		
		
		//Create and persist any new Domain objects
		try {
			Host host = createHost(facts);
			Release release = createRelease(facts);

			//Create a new deployment record.
			Deployment deployment = new Deployment();
			deployment.setDuration(report.getTotalTime());
			deployment.setHost(host);
			
			JsonNode previousRelease = facts.get("ftse_previous_release");
			deployment.setInstallPath(installPath);
			deployment.setPreviousReleaseId(previousRelease == null ? "Unknown" : previousRelease.asText());
			deployment.setPuppetMaster(facts.get("ftse_puppetmaster").asText());
			deployment.setRelease(release);
			deployment.setTime(report.time);
		
			Dao<Deployment, String> dao = DaoManager.createDao(connectionSource, Deployment.class);
			dao.create(deployment);
			
		} catch (SQLException e) {
			String message = "Error persisting Deployment information.";
			logger.error(message, e);
			resp.getWriter().append(message);
			resp.setStatus(500);
			
		}
	}

	/**
	 * This method converts the generic JsonNode object into a Release domain object.
	 * It then adds it to the derby database using ORMLite to convert from a POJO into a new database row.
	 */
	private Release createRelease(JsonNode facts) throws SQLException{
		Release release = new Release(facts.get("ftse_current_release").asText());
		JsonNode branch = facts.get("ftse_release_branch");
		JsonNode commitDate = facts.get("ftse_last_commit_date");
		JsonNode author = facts.get("ftse_last_commit_author");
		release.setGitBranch(branch == null ? "Unknown" : branch.asText());
		release.setCommitDate(commitDate == null ? "Unknown" : commitDate.asText());
		release.setAuthor(author == null ? "Unknown" : author.asText());
		release.setSupportWorksNumber(release.deriveFNumber());
		
		Dao<Release, String> dao = DaoManager.createDao(connectionSource, Release.class);
		dao.createIfNotExists(release);
			
		return release;
	}

	private Host createHost(JsonNode facts) throws SQLException {
		Host host = new Host(facts.get("hostname").asText(), facts.get("environment").asText());
		Dao<Host, String> hostDao = DaoManager.createDao(connectionSource, Host.class);
		hostDao.createIfNotExists(host);
		return host;
	}

	/**
	 * This calls a puppetDB exposed webservice to retrieve facts in JSON format.
	 * Jackson is used to parse the results into a JsonNode object.  
	 */
	private JsonNode getFactsFromPuppetDB(String hostname) throws IOException {
		CloseableHttpClient httpclient = HttpClients.createDefault();
		//TODO this is hardcoded! Make as an argument to ServerStarter.
		HttpGet httpGet = new HttpGet("http://ukubs-q01-pma01:8080/facts/"+hostname);
		httpGet.addHeader("Accept", "application/json");
		
		CloseableHttpResponse response = httpclient.execute(httpGet);
		
		try {
		    HttpEntity entity1 = response.getEntity();
		    ObjectMapper mapper = new ObjectMapper();
		    JsonNode rootNode = mapper.readValue(entity1.getContent(), JsonNode.class);
		    
		    JsonNode facts = rootNode.get("facts");
		    
		    // do something useful with the response body
		    // and ensure it is fully consumed
		    EntityUtils.consume(entity1);
		    
		    return facts;
		} finally {
		    response.close();
		}

	}

	/**
	 * This uses SnakeYaml to convert the YAML posted to the server into puppet report objects.
	 * These are found in the com.ftse.puppet.rubydto package.
	 * 
	 * TypeDescriptions are added as a way to convert from a ruby object into a java object.
	 * 
	 */
	private Report getReportFromYaml(Reader reader) throws IOException {
		Constructor constructor = new Constructor();
		constructor.addTypeDescription(new TypeDescription(Report.class, "!ruby/object:Puppet::Transaction::Report"));
		constructor.addTypeDescription(new TypeDescription(ResourceStatus.class, "!ruby/object:Puppet::Resource::Status"));
		constructor.addTypeDescription(new TypeDescription(PuppetLog.class, "!ruby/object:Puppet::Util::Log"));
		constructor.addTypeDescription(new TypeDescription(TransactionEvent.class, "!ruby/object:Puppet::Transaction::Event"));
		constructor.addTypeDescription(new TypeDescription(Metric.class, "!ruby/object:Puppet::Util::Metric"));
		constructor.addTypeDescription(new TypeDescription(String.class, "!ruby/sym"));
		constructor.addTypeDescription(new TypeDescription(String.class, "!binary"));
		Yaml yaml = new Yaml(constructor);
		
		if(logger.isDebugEnabled()){
			BufferedReader br = new BufferedReader(reader);
			StringBuffer sb = new StringBuffer();
			String s = null;
			while((s = br.readLine()) != null){
				sb.append(s);
			}
			logger.debug("Yaml DUMP: " + sb.toString());
		}
		
		return yaml.loadAs(reader, Report.class);
	}
	
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		resp.setContentType("text/html");
		resp.getWriter().println("This is for posting Puppet Reports, use POST not GET");
	}
	
	@Override
	public void destroy() {
		super.destroy();
		try {
			connectionSource.close();
		} catch (SQLException e) {
			logger.error("Could not close Derby DB connection source.", e);
		}
	}

}
