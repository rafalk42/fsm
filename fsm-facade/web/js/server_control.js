var el = React.createElement;

var ServerControl = React.createClass({
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
				"Hello world from server control!"
			)
		);
	}
});