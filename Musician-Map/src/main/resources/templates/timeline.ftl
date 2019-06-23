<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html">
    <title>Musician-Biology</title>
    <link rel="shortcut icon" href="http://static.tmimgcdn.com/img/favicon.ico">
    <link rel="icon" href="http://static.tmimgcdn.com/img/favicon.ico">
    <link rel="stylesheet" type="text/css" media="all" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" media="all" href="../static/css/bootstrap-glyphicons.css">
    <link rel="stylesheet" type="text/css" media="all" href="../static/css/styles.css">
    <script type="text/javascript" src="../static/js/jquery-1.11.0.min.js"></script>
</head>

<body>
<div class="container">
    <header class="page-header">
        <h1>${musician.getMusician()}</h1>
    </header>
    <#if events??&&(events?size> 0)>
        <ul class="timeline">
            <#list events as event>
                <li>
                    <div class="tldate">${event.getTime()}</div>
                </li>
                <#if event_index%2==0>
                    <li>
                        <div class="tl-circ"></div>
                        <div class="timeline-panel">
                            <div class="tl-heading">
                                <h4>${event.getPeople()}</h4>
                                <p><small class="text-muted"><i class="glyphicon glyphicon-time"></i> ${event.getPlace()}</small></p>
                            </div>
                            <div class="tl-body">
                                <p>${event.getEvent()}</p>
                            </div>
                        </div>
                    </li>
                <#else>
                    <li class="timeline-inverted">
                        <div class="tl-circ"></div>
                        <div class="timeline-panel">
                            <div class="tl-heading">
                                <h4>${event.getPeople()}</h4>
                                <p><small class="text-muted"><i class="glyphicon glyphicon-time"></i> ${event.getPlace()}</small></p>
                            </div>
                            <div class="tl-body">
                                <p>${event.getEvent()}</p>
                            </div>
                        </div>
                    </li>
                </#if>
            </#list>
        </ul>
    <#else>
        <ul class="timeline">
            <#list allEvent as event>
                <li>
                    <div class="tldate">${event.getTime()}</div>
                </li>
                <#if event_index%2==0>
                    <li>
                        <div class="tl-circ"></div>
                        <div class="timeline-panel">
                            <div class="tl-heading">
                                <h4>${event.getPeople()}</h4>
                                <p><small class="text-muted"><i class="glyphicon glyphicon-time"></i> ${event.getPlace()}</small></p>
                            </div>
                            <div class="tl-body">
                                <p>${event.getEvent()}</p>
                            </div>
                        </div>
                    </li>
                <#else>
                    <li class="timeline-inverted">
                        <div class="tl-circ"></div>
                        <div class="timeline-panel">
                            <div class="tl-heading">
                                <h4>${event.getPeople()}</h4>
                                <p><small class="text-muted"><i class="glyphicon glyphicon-time"></i> ${event.getPlace()}</small></p>
                            </div>
                            <div class="tl-body">
                                <p>${event.getEvent()}</p>
                            </div>
                        </div>
                    </li>
                </#if>
            </#list>
        </ul>
    </#if>
</div>
</body>

</html>