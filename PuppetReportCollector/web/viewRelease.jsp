<%@page import="com.ftse.puppet.domain.Release"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<html>
<head>
	<title>FTSE Release Management</title>
	<link rel="stylesheet" href="static/style.css">
</head>
<body>
<jsp:useBean id="entitySelector" scope="application" class="com.ftse.puppet.web.ReportView"/>

<h1> FTSE Release Management </h1>

<p> Release details for release with ID <b>${param.releaseId}</b> </p> 
<%
Release release = entitySelector.getReleaseById(request.getParameter("releaseId"));

if (release == null){
%>
	<br/><p style="color:red"> No Release found </p>
<%
} else {

	request.setAttribute("release", release);
%>
<table style="width:500px">
	<tr> <td> Git Branch </td> <td> ${release.gitBranch} </td> </tr>
	<tr> <td> Author </td> <td> ${release.author} </td> </tr>
	<tr> <td> Commit Date </td> <td> ${release.commitDate} </td> </tr>
	<tr> <td> SupportWorks Number </td> <td> ${release.supportWorksNumber} </td> </tr>
</table>
<% } %>