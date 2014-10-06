package com.ftse.puppet.domain;

import java.math.BigDecimal;
import java.math.RoundingMode;

import com.j256.ormlite.field.DatabaseField;
import com.j256.ormlite.table.DatabaseTable;

@DatabaseTable
public class Deployment {

	@DatabaseField(columnName="ID", generatedId = true)
	private int id;
	
    @DatabaseField(columnName="HOST_ID", canBeNull = false, foreign = true)
	private Host host;
	
	@DatabaseField(columnName="RELEASE_ID", canBeNull = false, foreign = true)
	private Release release;
	
	@DatabaseField(columnName = "PREVIOUS_RELEASE_ID")
	private String previousReleaseId;
	
	@DatabaseField(columnName = "INSTALL_TIME", canBeNull = false)
	private String time;
	
	@DatabaseField(columnName = "DURATION", canBeNull = false)
	private double duration;
	
	@DatabaseField(columnName = "INSTALL_PATH")
	private String installPath;
	
	@DatabaseField(columnName = "PUPPETMASTER", canBeNull = false)
	private String puppetMaster;

	private boolean rolledBack;
	
	public Deployment(){
		
	}
	
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}
	
	public Host getHost() {
		return host;
	}
	
	public void setHost(Host host) {
		this.host = host;
	}
	
	public Release getRelease() {
		return release;
	}
	
	public void setRelease(Release release) {
		this.release = release;
	}
	
	public String getPreviousReleaseId() {
		return previousReleaseId;
	}
	
	public void setPreviousReleaseId(String previousReleaseId) {
		this.previousReleaseId = previousReleaseId;
	}
	
	public String getTime() {
		return time;
	}
	
	public void setTime(String time) {
		this.time = time;
	}
	
	public double getDuration() {
		return duration;
	}
	
	public String getDurationRounded() {
		BigDecimal bd = new BigDecimal(duration);
		bd = bd.setScale(2, RoundingMode.HALF_UP);
		return bd.toString() + " s";
	}
	
	public void setDuration(double duration) {
		this.duration = duration;
	}
	
	public String getInstallPath() {
		return installPath;
	}
	
	public void setInstallPath(String installPath) {
		this.installPath = installPath;
	}
	
	public String getPuppetMaster() {
		return puppetMaster;
	}
	
	public void setPuppetMaster(String puppetMaster) {
		this.puppetMaster = puppetMaster;
	}

	public boolean isRolledBack() {
		return rolledBack;
	}

	public void setRolledBack(boolean rolledBack) {
		this.rolledBack = rolledBack;
	}
	
}
