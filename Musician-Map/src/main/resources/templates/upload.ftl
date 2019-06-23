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
    <link rel="stylesheet" type="text/css" media="all" href="../static/css/laydate.css">
    <style>
        body {
            padding-top: 80px;
            padding-right: 100px;
        }

        .demo-footer a {
            padding: 0 5px;
            color: #01AAED;
        }
    </style>
    <script type="text/javascript" src="../static/js/jquery-1.11.0.min.js"></script>
    <script type="text/javascript" src="../static/js/laydate.js"></script>
</head>

<body>
<div class="container">
    <div class="row clearfix">
        <div class="col-md-1 column">
        </div>
        <div class="col-md-6 column">
            <img width="600" src="../static/img/background.png" />
        </div>

        <div class="col-md-1 column">
        </div>
        <div class="col-md-4 column" style="padding-top: 40px;">
            <div class="jumbotron" style="height: 500px;">
                <form role="form" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="name">音乐家姓名：</label>
                        <input type="text" name="musician" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="test1">轨迹起点：</label>
                        <input type="text" name="startTime" class="form-control" placeholder="请选择日期"
                               id="test1">
                        <script>
                            laydate.render({
                                elem: '#test1'
                            });
                        </script>
                    </div>
                    <div class="form-group">
                        <label for="test2">轨迹终点：</label>
                        <input type="text" name="endTime" class="form-control" placeholder="请选择日期"
                               id="test2">
                        <script>
                            laydate.render({
                                elem: '#test2'
                            });
                        </script>
                    </div>

                    <div class="form-group" style="padding-top:30px;">
                        <label for="exampleInputFile">输入文件：</label>
                        <input id="exampleInputFile" type="file" name="file" accept=".txt" />
                        <p class="help-block " style="font-size: 12px; ">
                            请输入后缀名为txt的文件。
                        </p>
                    </div>
                    <div style="padding-top:40px;float: right;">
                        <button class="btn btn-primary btn-large" type="submit">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>


</body>

</html>