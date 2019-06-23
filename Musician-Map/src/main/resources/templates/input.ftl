<!DOCTYPE HTML>
<html xmlns="http://www.w3.org/1999/html">

<head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html">
    <title>Musician</title>
    <link rel="shortcut icon" href="http://static.tmimgcdn.com/img/favicon.ico">
    <link rel="icon" href="http://static.tmimgcdn.com/img/favicon.ico">
    <link rel="stylesheet" type="text/css" media="all" href="../static/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" media="all" href="../static/css/bootstrap-glyphicons.css">
    <link rel="stylesheet" type="text/css" media="all" href="../static/css/styles.css">
    <script type="text/javascript" src="../static/js/jquery-1.11.0.min.js"></script>
    <style>
        .color_0 {
            background: #16a085;
            color: #fff
        }

        .color_1 {
            background: #27ae60;
            color: #fff
        }

        .color_2 {
            background: #2980b9;
            color: #fff
        }

        .color_3 {
            background: #f1c40f;
            color: #fff
        }

        .color_4 {
            background: #e67e22;
            color: #fff
        }

        .color_5 {
            background: #e74c3c;
            color: #fff
        }

    </style>
</head>

<body>
<div class="container">
    <div class="row clearfix" style="padding-top: 8%">
        <div class="col-md-6 column">
            <img width="600" src="../static/img/background.png" />
        </div>

        <div class="col-md-1 column">
        </div>
        <div class="col-md-5 column">
            <div class="jumbotron" style="height: 520px;">
                <form role="form" method="post">
                    <div class="btn-group">
                        <select class="form-control" name="select" style="width: 260px">
                            <option  value="请选择一位音乐家">请选择一位音乐家</option>
                            <#list musicians as mus>
                            <option value="${mus}">${mus}</option>
                            </#list>
                        </select>
                    </div>
                    <input class="btn btn-primary btn-large" type="submit" value="Start" style="float: right">
                    <div class="jumbotron" style="padding: 20px; margin: 10px 0">
                        <#list musician as str>
                           <button type="submit" name="str" value="${str}" class="btn btn-default color_${str_index}" style="margin: 0 20% 6% 0">${str}</button>
                        </#list>
                    </div>
                    <div  class="btn-group" style="float: right;">
                        <input class="btn btn-primary btn-large" type="submit" value="Next Page" name="str">
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</body>

</html>