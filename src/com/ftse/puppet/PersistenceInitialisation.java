package com.ftse.puppet;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.SQLException;
import java.util.Arrays;

import org.apache.log4j.Logger;

import com.ftse.puppet.domain.ScriptRun;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.DaoManager;
import com.j256.ormlite.db.DatabaseType;
import com.j256.ormlite.db.DerbyEmbeddedDatabaseType;
import com.j256.ormlite.jdbc.JdbcPooledConnectionSource;
import com.j256.ormlite.table.TableUtils;

public class PersistenceInitialisation {

	private static final Logger logger = Logger.getLogger(PersistenceInitialisation.class);
	private JdbcPooledConnectionSource connectionSource;
	private String scriptsDir = "scripts/";
	
	public PersistenceInitialisation(String databaseName){
		String connectionURL = "jdbc:derby:"+databaseName+";create=true";
		try {
			DatabaseType databaseType = new DerbyEmbeddedDatabaseType();
			connectionSource = new JdbcPooledConnectionSource(connectionURL, databaseType);
			// only keep the connections open for 1 minute
			connectionSource.setMaxConnectionAgeMillis(60 * 1000);
		}  catch (Throwable e)  {
			logger.error("createDatabase: Error creating a connection to local DB.", e);
			System.exit(-1);
		}
	}

	public JdbcPooledConnectionSource getConnectionSource() {
		return connectionSource;
	}

	/**
	 * A mechanism for altering schema or data of the report DB.
	 * Runs any scripts it finds in scriptsDir (scripts/ by default) that have not been run prior. 
	 */
	public void runInitialScripts() throws SQLException, IOException {
		Dao<ScriptRun, String> dao = DaoManager.createDao(getConnectionSource(), ScriptRun.class);
		if(!dao.isTableExists()){
			TableUtils.createTable(getConnectionSource(), ScriptRun.class);
		}

		File root = new File(scriptsDir);
		if(!root.exists()){
			logger.error("No scripts directory found - Database tables can not be initialised. Please install properly.");
			System.exit(-1);
		}
		File[] listedFiles = root.listFiles();
		Arrays.sort(listedFiles);
		for(File script : listedFiles){
			if(dao.idExists(script.getName())){
				continue;
			}
			String rawSQL = readFile(script.getAbsolutePath());
			dao.executeRawNoArgs(rawSQL);
			ScriptRun run = new ScriptRun(script.getName());
			dao.createIfNotExists(run);
		}
	}

	private String readFile(String path) throws IOException {
		byte[] encoded = Files.readAllBytes(Paths.get(path));
		return new String(encoded, Charset.defaultCharset());
	}

	public void setScriptsDir(String scriptsDir) {
		this.scriptsDir = scriptsDir;
	}

}
