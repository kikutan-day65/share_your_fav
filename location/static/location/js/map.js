class MapManager {
    constructor(initLatitude, initLongitude, zoomLevel = 13) {
        this.map = L.map("map").setView(
            [initLatitude, initLongitude],
            zoomLevel
        );
        this.initializeMap();
        this.initializeSidebar();
        this.initializeCustomPopup();
    }

    initializeMap() {
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 18,
            attribution: "Map data &copy; OpenStreetMap contributors",
        }).addTo(this.map);
    }

    initializeSidebar() {
        this.sidebar = L.control
            .sidebar({ container: "sidebar" })
            .addTo(this.map)
            .open("home");

        this.sidebar.on("content", (ev) => {
            switch (ev.id) {
                case "autopan":
                    this.sidebar.options.autopan = true;
                    break;
                default:
                    this.sidebar.options.autopan = false;
            }
        });
    }

    initializeCustomPopup() {
        this.customPopup = L.control.customPopup("custom-popup", {
            position: "left",
            closeButton: true,
            autopan: true,
        });
    }

    showMarkers(locations) {
        locations.forEach((location) => {
            const marker = L.marker([
                location.fields.latitude,
                location.fields.longitude,
            ]).addTo(this.map);

            marker.on("click", () => {
                this.customPopup.addTo(this.map);
                this.customPopup.show();
            });
        });
    }
}

class CustomPopup extends L.Evented {
    constructor(div_id, options) {
        super();
        L.setOptions(this, options);

        // Find content container
        var content = (this._contentContainer = L.DomUtil.get(div_id));
        console.log(div_id);

        // Remove the content container from its original parent
        if (content.parentNode != undefined) {
            content.parentNode.removeChild(content);
        }

        var l = "leaflet-";

        // Create sidebar container
        // leaflet-customPopup-leftみたいになる
        var container = (this._container = L.DomUtil.create(
            "div",
            l + "customPopup " + this.options.position
        ));

        // Style and attach content container
        L.DomUtil.addClass(content, l + "control");
        container.appendChild(content);

        // Create close button and attach it if configured
        if (this.options.closeButton) {
            var close = (this._closeButton = L.DomUtil.create(
                "a",
                "close",
                container
            ));
            close.innerHTML = "&times;";
        }
    }

    addTo(map) {
        var container = this._container;
        var content = this._contentContainer;

        // Attach event to close button
        if (this.options.closeButton) {
            var close = this._closeButton;

            L.DomEvent.on(close, "click", this.hide, this);
        }

        // 'transitionend' イベントリスナーをサイドバーのコンテナに設定
        // transitionend: CSSの遷移（アニメーション）が終了したときに発火するイベント
        L.DomEvent.on(
            container,
            "transitionend", // アニメーションが終了したときのイベント
            this._handleTransitionEvent, // アニメーション終了後に呼ばれるメソッド
            this
        ).on(
            container,
            "webkitTransitionEnd", // webkit系のブラウザ用に遷移終了イベントを設定
            this._handleTransitionEvent, // 同様にアニメーション終了後に呼ばれるメソッド
            this
        );

        // Attach sidebar container to controls container
        var controlContainer = map._controlContainer;
        controlContainer.insertBefore(container, controlContainer.firstChild);

        this.map = map;

        // Make sure we don't drag the map when we interact with the content
        var stop = L.DomEvent.stopPropagation;
        var fakeStop = L.DomEvent._fakeStop || stop;
        L.DomEvent.on(content, "contextmenu", stop)
            .on(content, "click", fakeStop)
            .on(content, "mousedown", stop)
            .on(content, "touchstart", stop)
            .on(content, "dblclick", fakeStop)
            .on(content, "mousewheel", stop)
            .on(content, "wheel", stop)
            .on(content, "scroll", stop)
            .on(content, "MozMousePixelScroll", stop);

        return this;
    }

    removeFrom(map) {
        //if the control is visible, hide it before removing it.
        this.hide();

        var container = this._container;
        var content = this._contentContainer;

        // Remove sidebar container from controls container
        var controlContainer = map._controlContainer;
        controlContainer.removeChild(container);

        //disassociate the map object
        this._map = null;

        // Unregister events to prevent memory leak
        var stop = L.DomEvent.stopPropagation;
        var fakeStop = L.DomEvent._fakeStop || stop;
        L.DomEvent.off(content, "contextmenu", stop)
            .off(content, "click", fakeStop)
            .off(content, "mousedown", stop)
            .off(content, "touchstart", stop)
            .off(content, "dblclick", fakeStop)
            .off(content, "mousewheel", stop)
            .off(content, "wheel", stop)
            .off(content, "scroll", stop)
            .off(content, "MozMousePixelScroll", stop);

        L.DomEvent.off(
            container,
            "transitionend",
            this._handleTransitionEvent,
            this
        ).off(
            container,
            "webkitTransitionEnd",
            this._handleTransitionEvent,
            this
        );

        if (this._closeButton && this._close) {
            var close = this._closeButton;

            L.DomEvent.off(close, "click", this.hide, this);
        }

        return this;
    }

    isVisible() {
        return L.DomUtil.hasClass(this._container, "visible");
    }

    show() {
        if (!this.isVisible()) {
            L.DomUtil.addClass(this._container, "visible");
            if (this.options.autoPan) {
                this._map.panBy([-this.getOffset() / 2, 0], {
                    duration: 0.5,
                });
            }
            this.fire("show");
        }
    }

    hide(e) {
        if (this.isVisible()) {
            L.DomUtil.removeClass(this._container, "visible");
            if (this.options.autoPan) {
                this._map.panBy([this.getOffset() / 2, 0], {
                    duration: 0.5,
                });
            }
            this.fire("hide");
        }
        if (e) {
            L.DomEvent.stopPropagation(e);
        }
    }

    toggle() {
        if (this.isVisible()) {
            this.hide();
        } else {
            this.show();
        }
    }

    getContainer() {
        return this._contentContainer;
    }

    getCloseButton() {
        return this._closeButton;
    }

    setContent(content) {
        var container = this.getContainer();

        if (typeof content === "string") {
            container.innerHTML = content;
        } else {
            // clean current content
            while (container.firstChild) {
                container.removeChild(container.firstChild);
            }

            container.appendChild(content);
        }

        return this;
    }

    getOffset() {
        if (this.options.position === "right") {
            return -this._container.offsetWidth;
        } else {
            return this._container.offsetWidth;
        }
    }

    _handleTransitionEvent(e) {
        if (e.propertyName == "left" || e.propertyName == "right")
            this.fire(this.isVisible() ? "shown" : "hidden");
    }
}

// ファクトリー関数 (CustomPopup インスタンスを作成)
L.control.customPopup = function (div_id, options) {
    return new CustomPopup(div_id, options);
};

export { MapManager };
