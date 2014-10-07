package com.ftse.puppet;

import java.net.URL;

import org.apache.jasper.servlet.JspServlet;
import org.apache.log4j.Logger;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.DefaultServlet;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.webapp.WebAppContext;

/**
 * 
 * The main class for starting the Jetty web server and Derby database 
 * 
 * @author aimana
 *
 */
public class ServerStarter {
	
	private static final Logger logger = Logger.getLogger(ServerStarter.class);
 
    public static void main(String[] args) throws Exception {
    	logger.info("Initialising database connection pool");
    	PersistenceInitialisation initialiser = PersistenceInitialisationFactory.get("reportDb");
    	
    	//This runs the scripts that haven't been run yet in the scripts/ directory, useful for
    	//altering schema or performing data modification on a live database without running SQL manually. 
    	initialiser.runInitialScripts();
    	
    	//Required for JSP compilation.
    	System.setProperty("org.apache.jasper.compiler.disablejsr199","true");
    	
    	//TODO make this configurable
    	int port = 8100;
    	logger.info("Starting Jetty server on port " + port);
        Server server = new Server(port);
        
        //Try to find out if we are running off the filesystem (i.e. in Eclipse) or from a Jar as 
        // this will affect how our resource base is defined.
        URL resource = ServerStarter.class.getClassLoader().getResource("web");
        String uri = "web/";
		if(resource != null){
			uri = resource.toExternalForm();
		}

        //JSP context
        WebAppContext webAppContext = new WebAppContext();
        webAppContext.setContextPath("/");
        webAppContext.setResourceBase(uri);
        server.setHandler(webAppContext);
        
        //Root context
        ServletHolder holderDefault = new ServletHolder("default", DefaultServlet.class);
        holderDefault.setInitParameter("resourceBase", uri);
        holderDefault.setInitParameter("dirAllowed", "false");
        webAppContext.addServlet(holderDefault, "/");
        
        //Servlet context
        PuppetReportCollector puppetReportCollector = new PuppetReportCollector(initialiser.getConnectionSource());
		webAppContext.addServlet(new ServletHolder(puppetReportCollector),"/upload/*");
		webAppContext.addServlet(new ServletHolder("jsp", JspServlet.class),"*.jsp");
		
        server.start();
        server.join();
    }

}