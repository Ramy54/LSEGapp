package com.ftse.puppet.rubydto;

import java.util.List;
import java.util.Map;

public class Report {

	public Long configuration_version;
	public String time;
	public Map<String, ResourceStatus> resource_statuses;
	public int report_format;
	public String status;
	public String environment;
	public String kind;
	public String host;
	public List<PuppetLog> logs;
	public Map<String, Metric> metrics;
	public String puppet_version;
	
	public double getTotalTime() {
		Metric timeMetric = metrics.get("time");
		if(timeMetric == null){
			return 0;
		}
		List<String[]> times = timeMetric.values;
		for(String[] s : times){
			if(s[0].equals("total")){
				return Double.parseDouble(s[2]);
			}
		}
		return 0;
	}

}
