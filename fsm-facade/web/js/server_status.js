var el = React.createElement;

var ServerStatus = React.createClass({
	getInitialState: function ()
	{
		return ({
		});
	},
	
	render: function ()
	{
		return (
			el(
				"span",
				null,
				"Hello world from server status!"
			)
		);
	}
});