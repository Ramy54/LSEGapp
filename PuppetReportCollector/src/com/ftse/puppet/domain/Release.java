package com.ftse.puppet.domain;

import java.util.Collection;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.j256.ormlite.field.DatabaseField;
import com.j256.ormlite.field.ForeignCollectionField;
import com.j256.ormlite.table.DatabaseTable;

@DatabaseTable
public class Release {

	@DatabaseField(columnName="ID", id = true)
	private String id;
	
	@DatabaseField(columnName = "GIT_BRANCH")
	private String gitBranch;
	
	@DatabaseField(columnName = "AUTHOR")
	private String author;
	
	@DatabaseField(columnName = "COMMIT_DATE")
	private String commitDate;

	@DatabaseField(columnName = "SUPPORT_WORKS_NUMBER")
	private String supportWorksNumber;
	
	@ForeignCollectionField(eager = false, orderColumnName="INSTALL_TIME")
	private Collection<Deployment> deployments;
	
	public Release(){}
	
	public Release(String id) {
		this.id = id;
	}

	public String getId() {
		return id;
	}
	
	public void setId(String id) {
		this.id = id;
	}
	
	public String getGitBranch() {
		return gitBranch;
	}
	
	public void setGitBranch(String gitBranch) {
		this.gitBranch = gitBranch;
	}
	
	public String getSupportWorksNumber() {
		return supportWorksNumber;
	}
	
	public String getAuthor() {
		return author;
	}

	public void setAuthor(String author) {
		this.author = author;
	}

	public String getCommitDate() {
		return commitDate;
	}

	public void setCommitDate(String commitDate) {
		this.commitDate = commitDate;
	}
	
	public Collection<Deployment> getDeployments() {
		return deployments;
	}
	
	public String deriveFNumber() {
		String ret;
		//Try to derive it from the Tag if possible.
		ret = parseFNumberFromString(id);
		if(ret == null){
			//If the tag doesn't have it, try the branch name.
			ret = parseFNumberFromString(gitBranch);
		} 
		//Still nothing? Give up.
		if(ret == null){
			ret = "Unknown";
		}
		
		return ret;
	}

	private String parseFNumberFromString(String s) {
		if(s == null){
			return s;
		}
		
		Pattern pat = Pattern.compile("F0[0-9]{6,6}");
	    Matcher matcher = pat.matcher(s);
		
		if(matcher.find()){
			return matcher.group(0);
		}
		return null;
	}

	public void setSupportWorksNumber(String supportWorksNumber) {
		this.supportWorksNumber = supportWorksNumber;
	}

	
}
