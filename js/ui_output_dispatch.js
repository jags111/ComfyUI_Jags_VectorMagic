export function registerUiOutputListener(nodeType, nodeData, message_type, func) {
	if (nodeData?.ui_output?.includes(message_type) || nodeData?.description?.includes(message_type)) {
		const onExecuted = nodeType.prototype.onExecuted;
		nodeType.prototype.onExecuted = function (message) {
			onExecuted?.apply(this, arguments);
			if (message[message_type]) {
				var the_message = message[message_type];
				var node = undefined;
				if (typeof the_message[0] === 'string' && the_message[0].startsWith('id=')) {
					node = this.graph._nodes_by_id[the_message[0].slice(3)];
					the_message.splice(0,1);
				} else {
					node = this;
				}
				func.apply(node, [the_message]);
			}
		};
	}
};