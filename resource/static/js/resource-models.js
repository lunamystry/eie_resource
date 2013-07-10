(function() {
  var Resource = {};
  window.Resource = Resource;

  Resource.Session = Backbone.Model.extend({
    urlRoot: "/sessions",
    idAttribute: "_id",
    key: function() { return this.get("name"); },
    username: function() { return "username"; },
    timeout: function() { return "timeout"; },
  });

  Resource.User = Backbone.Model.extend({
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

  Resource.Users = Backbone.Collection.extend({
    url: "/users",
    model: Resource.User,
    parse: function(response){
      return response.result;
    }
  });

  Resource.Group = Backbone.Model.extend({
    idAttribute: "_id",
    name: function() { return this.get("name"); },
    members: function() { return "MEMBERS LIST"; },
  });

  Resource.Groups = Backbone.Collection.extend({
    url: "/groups",
    model: Resource.Group,
    parse: function(response){
      return response.result;
    }
  });

})()
