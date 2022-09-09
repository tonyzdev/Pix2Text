# coding: utf-8
# Copyright (C) 2022, [Breezedeus](https://github.com/breezedeus).

def render_html(newest_fp, image_type, text, out_html_fp):
    html_str = """
<!DOCTYPE html>
<html>
  <head>
    <link
      rel="stylesheet"
      href="https://cindyjs.org/dist/v0.8/katex/katex.min.css"
    />
    <script
      type="text/javascript"
      src="https://cindyjs.org/dist/v0.8/katex/katex.min.js"
    ></script>
    <script
      type="text/javascript"
      src="https://cindyjs.org/dist/v0.8/webfont.js"
    ></script>
    <style>
      body {
        /* background-color: rgb(154, 183, 249); */
      }
      #latex {
        min-height: auto;
        margin-left: auto;
        margin-right: auto;
        width: 760px;
      }

      #textarea {
        margin-left: auto;
        margin-right: auto;
        display: block;
      padding: 16px;
        /* height: 200px; */
      }

      body {
        display: flex;
        flex-direction: column;
        align-items: center;
      }

      .img-container {
        max-width: 760px;
      }
      .img-container img {
        max-width: 100%
      }
            .row {
        display: flex;
        gap: 1em;
        width: 760px;
      }
      .row textarea {
        flex: 1;
      }
      .row .col {
        width: 80px;
        display: flex;
        flex-direction: column;
        gap: 0.5em;
      }

      .container {
        width: 760px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      .container .refresh {
        position: absolute;
        right: 0;
        top: 0;
        padding: 4px 8px;
      }
      .btn {
        font-size: 16px;
        padding: 4px 6px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        color: rgb(62, 59, 59)
      }
      .cp {
        background-color: #f07878;
      }
      .cpd {
        background-color:   #a7d797;
      }
      .cpdd {
        background-color: #74a7f9;
      }
    </style>
  </head>

  <body class="with-footer">
    <div class="container">
    <h2 align="center">待解析图片</h2>
    <div class="img-container">
    """
    html_str += fr'<img src="{newest_fp}" />' + '\n </div>'
    html_str += """
    <button class="refresh btn" onClick="document.location.reload()">🔄 刷新</button>
    </div>
    <hr />

    <h2 align="center">解析结果</h2>
    """
    html_str += fr'<b>Image Type: </b> <div style="background:#ff9900;font-weight:bolder"> {image_type} </div>' + '\n'

    if image_type == 'formula':
        html_str += '<div id="latex"></div>'

    html_str += """

    <hr>

    <div class="row">

    """

    html_str += '\n<textarea id="textarea" rows="10">' + fr"{text}" + '</textarea>'

    html_str += """
          <div class="col">
        <button class="btn cp" type="button" onclick="copyTex()">复制</button>
        <button class="btn cpd" type="button" onclick="copyTexD()">$复制$</button>
        <button class="btn cpdd" type="button" onclick="copyTexDD()">$$复制$$</button>
      </div>
    </div>


    <script type="text/javascript">
      const textarea = document.querySelector("#textarea");
      const render = () => {
        var elt = document.createElement("div");
        elt.id = "latex";
        try {
          katex.render(textarea.value, elt, { displayMode: "display" });
        } catch (err) {
          console.error(err);
        }
        document.body.replaceChild(elt, document.querySelector("#latex"));
      };

      textarea.onblur = render;
      render();
    </script>

    <script type="text/javascript">
      function copy(text) {
        navigator.permissions
          .query({ name: "clipboard-write" })
          .then((result) => {
            if (result.state == "granted" || result.state == "prompt") {
              navigator.clipboard.writeText(text).then(() => {
                /* do nothing */
              });
            }
          });
      }
      function copyTex() {
        const texText = document.querySelector("#textarea").textContent;
        copy(texText);
      }
      function copyTexD() {
        const texText = document.querySelector("#textarea").textContent;
        copy(`$${texText}$`);
      }
      function copyTexDD() {
        const texText = document.querySelector("#textarea").textContent;
        copy(`$$${texText}$$`);
      }
    </script>

    <script>
      (async function callApi() {
        const resp = await fetch('/api/ocr')
        const data = await resp.json()
        console.log(data)
      })()
    </script>
  </body>
</html>
    """

    with open(out_html_fp, 'w') as f:
        f.writelines(html_str)