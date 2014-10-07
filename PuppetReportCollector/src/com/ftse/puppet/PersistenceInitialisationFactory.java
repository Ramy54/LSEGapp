package com.ftse.puppet;

import java.util.HashMap;
import java.util.Map;

/**
 * This is effectively a pool of singleton connections to each database. In practice this is used
 * only once when running live, but it is useful to have for unit tests.
 * 
 * Would prefer to use Dependency Injection but that seems overkill for this little project.
 * 
 * @author aimana
 */
public class PersistenceInitialisationFactory {

	static Map<String, PersistenceInitialisation> pis = new HashMap<String, PersistenceInitialisation>();
	
	public static PersistenceInitialisation get(String databaseName){
		if(pis.containsKey(databaseName)){
			return pis.get(databaseName);
		}
		PersistenceInitialisation pi = new PersistenceInitialisation(databaseName);
		pis.put(databaseName, pi);
		return pi;
	}
	
}
