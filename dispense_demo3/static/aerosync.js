(function () {
    var t = function (t) {
      (this.options = t || {}),
        this.options.onLoad || (this.options.onLoad = function () {}),
        this.options.onClose || (this.options.onClose = function () {}),
        this.options.onSuccess || (this.options.onSuccess = function () {}),
        this.options.onEvent || (this.options.onEvent = function () {}),
        this.options.onError || (this.options.onError = function () { }),
        (this.options.config = t.config || null),
        (this.configInitialized = !1),
        this.options.config
          ? window.addEventListener("message", this._handlePostMessage.bind(this))
          : window.addEventListener("message", this._onPostMessage.bind(this));
    };
    (t.prototype.launch = function () {
      var t;
      var path = ("?token=" + this.options.token) + 
                 (this.options.consumerId? "&consumerId=" + this.options.consumerId: "") + 
                 (this.options.deeplink? "&deeplink="+this.options.deeplink: "");
      var bg = (this.options.style && this.options.style.bgColor && this.options.style.opacity)? 
      (this.options.style.bgColor + ( Math.floor(this.options.style.opacity  * 255).toString(16))) : "#000000b2";
      (t = "local" == this.options.environment ? "http://localhost:8080/"+path
          : "staging" === this.options.environment
          ? "https://staging.aerosync.com/"+path
          : "production" === this.options.environment
          ? "https://www.aerosync.com/"+path
          : ""),
        (e = (this.options.style && this.options.style.width)?this.options.style.width: "375px"),
        (n = (this.options.style && this.options.style.height)?this.options.style.height: "688px"),
        (o = document.createElement("iframe")),
        (d = document.createElement("div")),
        (s = document.getElementById(this.options.id)),
        o.setAttribute("width", e),
        o.setAttribute("height", n),
        o.setAttribute("border", "0"),
        o.setAttribute("frame", "0"),
        o.setAttribute("frameborder", "0"),
        o.setAttribute("allowTransparency", "true"),
        o.setAttribute("src", t),
        o.setAttribute("marginheight", "0"),
        o.setAttribute("marginwidth", "0"),
        o.setAttribute("onload", this.options.onLoad()),
        o.setAttribute("title", this.options.iframeTitle, "Connect"),
        d.setAttribute("id", "widget-box"),
        (s.innerHTML = ""),
        s.appendChild(d);
      var i = document.getElementById("widget-box");
      (i.style.display = "flex"),
        (i.style.position = "fixed"),
        (i.style.width = "100%"),
        (i.style.left = "0"),
        (i.style.top = "0"),
        (i.style.backgroundColor = bg),
        (i.style.zIndex = "1"),
        (i.style.height = "100%"),
        (i.style.justifyContent = "center"),
        (i.style.alignItems = "center"),
        window.matchMedia("(max-height: 700px)").matches &&
          o.setAttribute("height", "95%"),
        (i.innerHTML = ""),
        i.appendChild(o),
        (this.iframeDetails = { iframe: o, targetElement: i }),
        this.options.config &&
          ((this.configInterval = setInterval(
            function () {
              this.configInitialized
                ? clearInterval(this.configInterval)
                : this._setClientConfig(this.options.config);
            }.bind(this),
            100
          )),
          setTimeout(
            function () {
              clearInterval(this.configInterval);
            }.bind(this)
          ));
    }),
      (t.prototype._onPostMessage = function (t) {
        var e = {};
        if (
          this.iframeDetails &&
          this.iframeDetails.iframe &&
          t.source === this.iframeDetails.iframe.contentWindow
        ) {
          try {
            e = JSON.parse(t.data);
          } catch (t) {
            console.warn("Error processing event", t);
          }
          e.type && this._handleEvent(e);
        }
      }),
      (t.prototype._handleEvent = function (t) {
        var e = {
          pageSuccess: { callback: this.options.onSuccess },
          widgetPageLoaded: { callback: this.options.onEvent },
          widgetLoaded: { callback: this.options.onLoad },
          widgetClose: { callback: this.options.onClose },
          widgetError: { callback: this.options.onError },
          initialized: {
            callback: function () {
              this.configInitialized = !0;
            }.bind(this),
          },
        }[t.type];
        ("widgetClose" != t.type && "bankAdded" != t.type) ||
          (document
            .querySelector('iframe[title="' + this.options.iframeTitle + '"]')
            .remove(),
          document.getElementById("widget-box").remove()),
          e.callback(t.payload);
      }),
      (t.prototype._setClientConfig = function (t) {
        t.hasOwnProperty("ce_user_id") && (t.ce_user_id = t.ce_user_id),
          t.hasOwnProperty("FILoginAcctId") &&
            (t.FILoginAcctId = t.FILoginAcctId),
          this._postMessageToAeroSync({
            type: "clientConfig",
            data: { connect: t },
          });
      }),
      (t.prototype._postMessageToAeroSync = function (t) {
        this.iframeDetails.iframe.contentWindow.postMessage(JSON.stringify(t));
      }),
      (window.AerosyncConnect = t);
  }.call(this));