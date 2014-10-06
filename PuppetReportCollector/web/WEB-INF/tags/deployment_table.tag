<%@tag import="java.util.Collection"%>
<%@tag import="com.ftse.puppet.domain.Deployment"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<%@ attribute name="release" required="false" type="java.lang.String" %>
<%@ attribute name="host" required="false" type="java.lang.String" %>
<jsp:useBean id="entitySelector" scope="application" class="com.ftse.puppet.web.ReportView"/>

<%
Collection<Deployment> deployments;
if(release != null){
	deployments = entitySelector.getDeploymentsForRelease(release);
} else {
	deployments = entitySelector.getDeploymentsForHost(host);
}
request.setAttribute("deployments", deployments);
%>
<table>
	<tr>
		<th> Host </th>
		<th> Release </th>
		<th> Previous Release </th>
		<th> Install Time </th>
		<th> Duration </th>
		<th> Install Path </th>
		<th> PuppetMaster </th>
	</tr>
<c:forEach var="deployment" items="${deployments}">
	<tr>
		<td> ${deployment.host.hostname} </td>
		<td>
			<c:if test="${deployment.rolledBack}">
				<img src="static/warning.png" alt="Rolled Back" style="height: 16px; width: 16px"/>
			</c:if> 
			<a href="viewRelease.jsp?releaseId=${deployment.release.id}">${deployment.release.id}</a>
		</td>
		<td> 
			<a href="viewRelease.jsp?releaseId=${deployment.previousReleaseId}">${deployment.previousReleaseId}</a> 
		</td>
		<td> ${deployment.time} </td>
		<td> ${deployment.durationRounded} </td>
		<td> ${deployment.installPath} </td>
		<td> ${deployment.puppetMaster} </td>
	</tr>
</c:forEach>
</table>


 