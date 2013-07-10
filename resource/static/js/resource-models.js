(function() {
  var Ehlane = {};
  window.Ehlane = Ehlane;

  Ehlane.Session = Backbone.Model.extend({
    urlRoot: "/sessions",
    idAttribute: "_id",
    key: function() { return this.get("name"); },
    username: function() { return "username"; },
    timeout: function() { return "timeout"; },
  });

  Ehlane.User = Backbone.Model.extend({
    idAttribute: "_id",
    fullname: function() { return this.get("first_name") + " " + this.get("last_name") ; },
    username: function() { return this.get("username"); },
    gender: function() { return this.get("gender"); },
    address: function() { return this.get("address"); },
    email: function() { return this.get("email"); },
    school: function() { return this.get("school"); },
    cellphone_no: function() { return this.get("cellphone_no"); },
    phone_no: function() { return this.get("phone_no"); },
    role_id: function() { return this.get("role_id"); },
  });

  Ehlane.Users = Backbone.Collection.extend({
    url: "/users",
    model: Ehlane.User,
    parse: function(response){
      return response.result;
    }
  });

  Ehlane.Group = Backbone.Model.extend({
    idAttribute: "_id",
    name: function() { return this.get("name"); },
    members: function() { return "MEMBERS LIST"; },
  });

  Ehlane.Groups = Backbone.Collection.extend({
    url: "/groups",
    model: Ehlane.Group,
    parse: function(response){
      return response.result;
    }
  });

})()
