package com.ftse.puppet;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import com.ftse.puppet.domain.Deployment;
import com.ftse.puppet.domain.Host;
import com.ftse.puppet.domain.Release;
import com.ftse.puppet.domain.ScriptRun;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.DaoManager;
import com.j256.ormlite.table.TableUtils;

public class PersistenceInitialisationTest {

	@Test
	public void testRunInitialScript() throws Exception {
		
		PersistenceInitialisation pi = PersistenceInitialisationFactory.get("testReportDb");
		pi.setScriptsDir("testScripts/");
		TableUtils.dropTable(pi.getConnectionSource(), Host.class, true);
		TableUtils.dropTable(pi.getConnectionSource(), Release.class, true);
		TableUtils.dropTable(pi.getConnectionSource(), Deployment.class, true);
		TableUtils.dropTable(pi.getConnectionSource(), ScriptRun.class, true);
		
		Dao<ScriptRun, String> dao = DaoManager.createDao(pi.getConnectionSource(), ScriptRun.class);
		Dao<Host, String> hostDao = DaoManager.createDao(pi.getConnectionSource(), Host.class);
		
		assertFalse(dao.isTableExists());
		assertFalse(hostDao.isTableExists());
		pi.runInitialScripts();
		assertEquals(1, dao.countOf());
		assertTrue(dao.isTableExists());
		assertTrue(hostDao.isTableExists());
		
		//Make sure that running it again doesn't rerun the SQL.
		pi.runInitialScripts();
		assertEquals(1, dao.countOf());
	}

}
