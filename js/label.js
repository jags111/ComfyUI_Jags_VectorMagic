import { app } from "../../../scripts/app.js";

const MARGIN = 4;
const FONT_PX = 10;
const ID_WIDGET_HEIGHT = FONT_PX + 2*MARGIN;

function get_label_position_style(ctx, widget_width, y) {
    const elRect = ctx.canvas.getBoundingClientRect();
    const transform = new DOMMatrix()
        .scaleSelf(elRect.width / ctx.canvas.width, elRect.height / ctx.canvas.height)
        .multiplySelf(ctx.getTransform())
        .translateSelf(MARGIN, MARGIN + y);

    return {
        transformOrigin: '0 0',
        transform: transform,
        left: `0px`, 
        top: "0px", 
        width: `${widget_width - MARGIN*2}px`,
        height: `${LiteGraph.NODE_WIDGET_HEIGHT - MARGIN*2}px`,
        position: "absolute",
    }
}

function get_label_div_style() {
    return {
        fontSize: `${FONT_PX}px`,
        textAlign: `center`,
        border: `thin solid black`,
    }
}

app.registerExtension({
	name: "cg.custom.label_widget",
    getCustomWidgets(app) {
        const SIZE = [80,ID_WIDGET_HEIGHT];
        return {
            LABEL(node, inputName, inputData, app) {
                const opts = (inputData.length>1) ? inputData[1] : {}
                var value = "";
                if (opts.value) {
                    if (opts.value === '__random__') value = Math.floor(Math.random() * 10000000);
                    else value = opts.value;
                }
                const widget = {
                    type: inputData[0],
                    name: inputName,
                    size: SIZE, 
                    _value : value,
                    get value() { return this._value;},
                    set value(newValue) {  },
                    draw(ctx, node, widget_width, y, widget_height) { 
                        Object.assign(this.inputEl.style, get_label_position_style(ctx, widget_width, y));
                    },
                    async serializeValue(nodeId,widgetIndex) { return this.value; }
                };
                widget.inputEl = document.createElement("div");
                widget.inputEl.appendChild(document.createTextNode(`${widget.name} ${widget.value}`));
                Object.assign(widget.inputEl.style, get_label_div_style());

                widget.parent = node;
                document.body.appendChild(widget.inputEl);

                node.addCustomWidget(widget);
                node.onRemoved = function () { this.widgets[0].inputEl.remove(); };
                return widget;
            }
        }

    }
});

