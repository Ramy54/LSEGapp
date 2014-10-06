package com.ftse.puppet.web;

import static org.junit.Assert.*;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;

import org.junit.Before;
import org.junit.Test;

import com.ftse.puppet.domain.Deployment;
import com.ftse.puppet.domain.Release;

public class ReportViewTest {

	private ReportView rv;
	private Collection<Deployment> deployments;

	@Before
	public void setup() throws SQLException{
		deployments = new ArrayList<Deployment>();
		rv = new ReportView();
	}
	
	@Test
	public void testRolledBackDeploymentsWithOneDeployment() {
		addRelease(new Release("F1234"));
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack());
	}
	
	private void addRelease(Release... releases) {
		for(Release r : releases){
			Deployment d = new Deployment();
			d.setRelease(r);
			deployments.add(d);
		}
	}

	//If a release is installed twice in succession that is not considered a rollback.
	@Test
	public void testRolledBackDeploymentsWithTwoDeploymentsOfTheSameRelease() {
		Release releaseA = new Release("F1234");
		addRelease(releaseA, releaseA);
		
		rv.determineRollbacks(deployments);
		Iterator<Deployment> it = deployments.iterator();
		
		assertFalse(it.next().isRolledBack());
		assertFalse(it.next().isRolledBack());
	}
	
	@Test
	public void testRolledBackDeploymentsWithTwoDeploymentsOfDifferingReleases() {
		addRelease(new Release("F1234"), new Release("F5678"));
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack());
		assertFalse(it.next().isRolledBack());
	}
	
	@Test
	public void testRolledBackDeploymentsWithThreeDeploymentsNoneRolledBack() {
		Release releaseA = new Release("F1234");
		Release releaseB = new Release("F5678");
		addRelease(releaseA, releaseB, releaseB);
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack());
		assertFalse(it.next().isRolledBack());
		assertFalse(it.next().isRolledBack());
	}
	
	@Test
	public void testRolledBackDeploymentsWithThreeDeploymentsOneRolledBack() {
		Release releaseA = new Release("F1234");
		Release releaseB = new Release("F5678");
		addRelease(releaseA, releaseB, releaseA); //B is rolled back as we went back to A.
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack());
		assertTrue(it.next().isRolledBack());
		assertFalse(it.next().isRolledBack());
	}
	
	@Test
	public void testRolledBackDeploymentsWithFourDeploymentsOneRolledBack() {
		Release releaseA = new Release("F1234");
		Release releaseB = new Release("F5678");
		Release releaseC = new Release("F1111");
		addRelease(	releaseA,
					releaseB,
					releaseC,
					releaseB); //C is rolled back as we went back to B.
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack()); 	//A
		assertFalse(it.next().isRolledBack());	//B
		assertTrue(it.next().isRolledBack());	//C
		assertFalse(it.next().isRolledBack());	//B
	}
	
	@Test
	public void testRolledBackDeploymentsWithFourDeploymentsTwoRolledBack() {
		Release releaseA = new Release("F1234");
		Release releaseB = new Release("F5678");
		Release releaseC = new Release("F1111");
		addRelease(	releaseA,
					releaseB,
					releaseC,
					releaseA); //Both B and C rolled back as we went back to A.
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack()); 	//A
		assertTrue(it.next().isRolledBack());	//B
		assertTrue(it.next().isRolledBack());	//C
		assertFalse(it.next().isRolledBack());	//A
	}
	
	@Test
	public void testRolledBackDeploymentsWithFiveDeploymentsTwoRolledBackNonSequential() {
		Release releaseA = new Release("F1234");
		Release releaseB = new Release("F5678");
		Release releaseC = new Release("F1111");
		
		//Both B and C rolled back as we went back to A twice.
		addRelease(	releaseA,
					releaseB, 
					releaseA, 
					releaseC, 
					releaseA);
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack()); 	//A
		assertTrue(it.next().isRolledBack());	//B
		assertFalse(it.next().isRolledBack());	//A
		assertTrue(it.next().isRolledBack());	//C
		assertFalse(it.next().isRolledBack());	//A
	}
	
	@Test
	public void testRolledBackDeploymentsWithRollBackReleaseAlsoRolledBack() {
		Release releaseA = new Release("F1234");
		Release releaseB = new Release("F5678");
		Release releaseC = new Release("F1111");
		
		//C got rolled back, and then B got rolled back.
		addRelease(	releaseA, 
					releaseB, 
					releaseC, 
					releaseB, 
					releaseA);
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack()); 	//A
		assertTrue(it.next().isRolledBack());	//B
		assertTrue(it.next().isRolledBack());	//C
		assertTrue(it.next().isRolledBack());	//B
		assertFalse(it.next().isRolledBack());	//A
	}
	
	@Test
	//Bit of an odd scenario
	public void testRolledBackDeploymentsRollingBackToRolledBackVersion() {
		Release releaseA = new Release("F1234");
		Release releaseB = new Release("F5678");
		Release releaseC = new Release("F1111");
		
		//B got rolled back, and then we installed C and rolled back to B.
		addRelease(	releaseA, 
					releaseB, 
					releaseA, 
					releaseC, 
					releaseB);
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack()); 	//A
		assertTrue(it.next().isRolledBack());	//B
		assertTrue(it.next().isRolledBack());	//A
		assertTrue(it.next().isRolledBack());	//C
		assertFalse(it.next().isRolledBack());	//B
	}
	
	@Test
	public void testRolledBackDeploymentsWithRollBackReleaseAlsoRolledBackAndThenInstalledAgain() {
		Release releaseA = new Release("F1234");
		Release releaseB = new Release("F5678");
		Release releaseC = new Release("F1111");
		
		//C got rolled back, and then B got rolled back.
		addRelease(	releaseA,
					releaseB, 
					releaseC, 
					releaseB, 
					releaseA, 
					releaseA, 
					releaseA);
		
		rv.determineRollbacks(deployments);
		
		Iterator<Deployment> it = deployments.iterator();
		assertFalse(it.next().isRolledBack()); 	//A
		assertTrue(it.next().isRolledBack());	//B
		assertTrue(it.next().isRolledBack());	//C
		assertTrue(it.next().isRolledBack());	//B
		assertFalse(it.next().isRolledBack());	//A
		assertFalse(it.next().isRolledBack());	//A
		assertFalse(it.next().isRolledBack());	//A
	}

}
