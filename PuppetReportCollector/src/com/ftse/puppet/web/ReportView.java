package com.ftse.puppet.web;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import com.ftse.puppet.PersistenceInitialisation;
import com.ftse.puppet.PersistenceInitialisationFactory;
import com.ftse.puppet.domain.Deployment;
import com.ftse.puppet.domain.Host;
import com.ftse.puppet.domain.Release;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.DaoManager;
import com.j256.ormlite.jdbc.JdbcPooledConnectionSource;

/**
 * Used by the JSPs to retrieve data.
 * @author aimana
 *
 */
public class ReportView {

	private Dao<Host, String> hostDao;
	private Dao<Release, String> releaseDao;

	public ReportView () throws SQLException{
		PersistenceInitialisation initialiser = PersistenceInitialisationFactory.get("reportDb");
		JdbcPooledConnectionSource cs = initialiser.getConnectionSource();
		releaseDao = DaoManager.createDao(cs, Release.class);
		hostDao = DaoManager.createDao(cs, Host.class);
	}
	
	public List<Host> getHosts() throws SQLException {
		List<Host> hosts = new ArrayList<Host>();
		hosts = hostDao.queryForAll();
		return hosts;
	}
	
	public List<Release> getReleases() throws SQLException {
		List<Release> releases = new ArrayList<Release>();
		releases = releaseDao.queryForAll();
		return releases;
	}
	
	public Collection<Deployment> getDeploymentsForRelease(String releaseId) throws SQLException {
		Release release = releaseDao.queryForId(releaseId);
		Collection<Deployment> deployments = release.getDeployments();
		determineRollbacks(deployments);
		return deployments;
	}
	
	public Collection<Deployment> getDeploymentsForHost(String hostId) throws SQLException {
		Host host = hostDao.queryForId(hostId);
		Collection<Deployment> deployments = host.getDeployments();
		determineRollbacks(deployments);
		return deployments;
	}
	
	public Release getReleaseById(String releaseId) throws SQLException {
		return releaseDao.queryForId(releaseId);
	}

	//Assuming these are ordered by install time
	public void determineRollbacks(Collection<Deployment> deployments) {
		Deployment[] deploymentArray = deployments.toArray(new Deployment[deployments.size()]);
		for(int i = 0; i < deploymentArray.length - 2; i++){
			for(int j = i + 2; j < deploymentArray.length; j++){
				if(deploymentArray[j].getRelease().getId().equals(deploymentArray[i].getRelease().getId())){
					//Everything between i and j non-inclusive should be considered rolled back,
					//UNLESS we have another i release in the middle - see 
					//testRolledBackDeploymentsWithFiveDeploymentsTwoRolledBackNonSequential
					int k = j - 1;
					while (k > i){
						if(deploymentArray[k].getRelease().getId().equals(deploymentArray[i].getRelease().getId())){
							k--;
							continue;
						}
						deploymentArray[k--].setRolledBack(true);
					}
				}
			}
		}
	}
	

}
