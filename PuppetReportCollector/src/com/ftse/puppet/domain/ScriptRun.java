package com.ftse.puppet.domain;

import com.j256.ormlite.field.DatabaseField;
import com.j256.ormlite.table.DatabaseTable;

@DatabaseTable
public class ScriptRun {

	@DatabaseField(id=true)
	private String name;

	public ScriptRun(){}
	public ScriptRun(String name) {
		this.name = name;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
}
