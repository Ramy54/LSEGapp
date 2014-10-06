package com.ftse.puppet.rubydto;

import java.util.List;

public class ResourceStatus {

	public String resource;
	public String file;
	public String line;
	public double evaluation_time;
	public int change_count;
	public int out_of_sync_count;
	public List<String> tags;
	public String time;
	public List<TransactionEvent> events;
	public boolean out_of_sync;
	public boolean changed;
	public String resource_type;
	public String title;
	public boolean skipped;
	public boolean failed;
	
}
