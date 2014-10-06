package com.ftse.puppet.domain;

import static org.junit.Assert.*;

import org.junit.Test;

public class ReleaseTest {

	@Test
	public void testGetSupportWorksNumberWithHashCommit() {
		Release r = new Release("ae17e2a6e002e0cf5e5f01789126575f9ee5d1af");
		assertEquals("Unknown", r.deriveFNumber());
	}
	
	@Test
	public void testGetSupportWorksNumberWithTag() {
		Release r = new Release("F0178912-20140604-ETL");
		assertEquals("F0178912", r.deriveFNumber());
	}
	
	@Test
	public void testGetSupportWorksNumberWithMistypedTag() {
		Release r = new Release("F01234567890-20140604-ETL");
		assertEquals("F0123456", r.deriveFNumber());
	}
	
	@Test
	public void testGetSupportWorksNumberWithCommitHashAndBranchSpecified() {
		Release r = new Release("ae17e2a6e002e0cf5e5f01789126575f9ee5d1af");
		r.setGitBranch("F0185055");
		assertEquals("F0185055", r.deriveFNumber());
	}
	
	//Prefer tag to branch name if they are both in the form F0xxxxxx
	@Test
	public void testGetSupportWorksNumberWithTagAndBranchSpecified() {
		Release r = new Release("F0178912-20140604-ETL");
		r.setGitBranch("F0185055");
		assertEquals("F0178912", r.deriveFNumber());
	}

}
