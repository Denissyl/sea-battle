import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '''<!doctype html>
                <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Глобальные стили</title>
        <style type="text/css">
            table {
                width:30%;
            }
            td {
                text-align: center;
                width:10%;
                position:relative;
            }
            td:after{
                content:'';
                display:block;
                margin-top:100%;
            }
            td .my_div {
                font-size: 20;
                position:absolute;
                padding-top: 70;
                top:0;
                bottom:0;
                left:0;
                right:0;
                background:white;
            }
 
        </style>
    </head>
    <head>
        <style type="text/css">
        a.button {display:block; height:100%; width:100%;}
        </style>
    </head>
    <body>
        <table border="2" align="left" style="margin-top:100px; margin-left:200px" cellspacing="0">
            
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
         </table>
    </body>
    <body>
        <table border="2" align="right" style="margin-top:100px; margin-right:200px" cellspacing="0">
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
            <tr>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
                <td><div class="my_div"><a href="#" class="button"></a></div></td>
            </tr>
         </table>
    </body>
</html>'''


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7000))
    app.run('0.0.0.0', port)
