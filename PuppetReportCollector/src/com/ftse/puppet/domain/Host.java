package com.ftse.puppet.domain;

import java.util.Collection;

import com.j256.ormlite.field.DatabaseField;
import com.j256.ormlite.field.ForeignCollectionField;
import com.j256.ormlite.table.DatabaseTable;

@DatabaseTable
public class Host {

	@DatabaseField(columnName="HOSTNAME", canBeNull = false, id = true)
	private String hostname;
	
	@DatabaseField(columnName="ENV", canBeNull = false)
	private String env;
	
	@ForeignCollectionField(eager = false, orderColumnName="INSTALL_TIME")
	private Collection<Deployment> deployments;
	
	public Host(){}
	
	public Host(String hostname, String env) {
		this.hostname = hostname;
		this.env = env;
	}
	
	public String getHostname() {
		return hostname;
	}
	public void setHostname(String hostname) {
		this.hostname = hostname;
	}
	public String getEnv() {
		return env;
	}
	public void setEnv(String env) {
		this.env = env;
	}

	public Collection<Deployment> getDeployments() {
		return deployments;
	}
	
}
