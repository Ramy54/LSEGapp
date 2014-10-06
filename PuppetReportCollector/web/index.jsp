<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib prefix="f" tagdir="/WEB-INF/tags" %>

<html>
<head>
	<title>FTSE Release Management</title>
	<link rel="stylesheet" href="static/style.css">
</head>
<body>

<jsp:useBean id="entitySelector" scope="application" class="com.ftse.puppet.web.ReportView"/>

<h1> FTSE Release Management </h1>

<p> Select a host or a release from the dropdowns to see more information about its release history and current status.</p>

<form style="max-width: 500px" action="index.jsp" method="GET">
	<table>
		<tr>
			<th> Host </th><th> Release</th>
		</tr>
		<tr>
			<td>
				<select name="hostSelect" id="hostSelect" style="width: 90%;" onchange="form.submit()">
					<c:forEach var="hostToSelect" items="${entitySelector.hosts}" >
						<option value="${hostToSelect.hostname}">${hostToSelect.hostname}</option>
					</c:forEach>
				</select> 
			</td>
			<td> 
				<select name="releaseSelect" id="releaseSelect" style="width: 90%;" onchange="form.submit()">
					<c:forEach var="releaseToSelect" items="${entitySelector.releases}" >
						<option value="${releaseToSelect.id}">${releaseToSelect.id}</option>
					</c:forEach>
				</select>
			</td>
		</tr>
	</table>
	
	<table>
	</table>
</form>

<script>
	document.getElementById("hostSelect").selectedIndex = -1;
	document.getElementById("releaseSelect").selectedIndex = -1;
</script>

<br/>
<c:set var="host" value="${param.hostSelect}" />
<c:set var="release" value="${param.releaseSelect}" />
<c:if test="${host != null}">
	<p> Deployments found for host <b>${host}</b> </p>
	<br/>
	<f:deployment_table host="${host}"/>
</c:if>
<c:if test="${release != null}">
	<p> Deployments found for release <b>${release}</b> </p>
	<br/>
	<f:deployment_table release="${release}"/>
</c:if>


</body>
</html>