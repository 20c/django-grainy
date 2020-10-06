(function() {

/* javascript implementation of grainy permissioning logic
 */


// permission flags

GRAINY_CONST = {
  PERM_DENY : 0,
  PERM_READ : 0x01,
  PERM_UPDATE : 0x02,
  PERM_CREATE : 0x04,
  PERM_DELETE : 0x08
}


GRAINY_CONST.PERM_WRITE = GRAINY_CONST.PERM_UPDATE |
                          GRAINY_CONST.PERM_CREATE |
                          GRAINY_CONST.PERM_DELETE


GRAINY_CONST.PERM_RW = GRAINY_CONST.PERM_READ |
                       GRAINY_CONST.PERM_WRITE


// mapping of int permission flags to string permission
// flags

GRAINY_CONST.PERM_STRING_MAP = {}
GRAINY_CONST.PERM_STRING_MAP[GRAINY_CONST.PERM_CREATE] = "c"
GRAINY_CONST.PERM_STRING_MAP[GRAINY_CONST.PERM_READ] = "r"
GRAINY_CONST.PERM_STRING_MAP[GRAINY_CONST.PERM_UPDATE] = "u"
GRAINY_CONST.PERM_STRING_MAP[GRAINY_CONST.PERM_DELETE] = "d"


/**
 * grainy permission functionality
 * @class grainy
 */

grainy = {

  /**
   * namespace delimiter
   * @property delimiter
   */

  delimiter : ".",

  /**
   * setup grainy with a set of permission rules
   * rules should be an object literal of
   * grainy namespace (`str`) -> permission flags (`int`)
   *
   * @method setup
   * @param {Object} rules
   */

  setup : function(rules) {
    this.flags = GRAINY_CONST.PERM_STRING_MAP
    this.rules = rules
    this.update_index()
  },

  /**
   * traverse the permissioning index and return the permission
   * flags valid for the supplied namespace path
   *
   * This is an internal method and should not be called manually
   *
   * Please use `check` instead.
   *
   * @method _check
   * @private
   * @param {Array} keys permissioning namespace path
   * @param {Object} branch
   * @param {Number} flags
   * @param {Number} i
   * @param {Boolean} explicit
   * @param {Number} l
   * @returns {Object} result
   */

  _check : function(keys, branch, flags, i, explicit, l) {
    var key = keys[i]

    if(key === undefined) {
      return {flags : flags, i: i }
    }

    var result = {}, result_wc = {}

    var leaf = branch[key], leaf_wc = branch["*"]

    if(!l)
      l = keys.length


    // current location in path exists as a direct
    // match

    if(leaf !== undefined) {
      if(explicit && leaf["__implicit"] && i+1 >= l) {

        // explicit matching only, permissioning rule
        // for path is only implied by child so we
        // bail

        result = {flags:0, i:0}
      } else {

        // process the next key of the namespace

        result = this._check(
          keys,
          leaf,
          leaf["__"] === undefined ? flags : leaf["__"],
          i+1,
          explicit,
          l
        )
      }
    }

    // current location in path exists as a wildcard `*`
    // match

    if(leaf_wc !== undefined) {
      if(explicit && leaf_wc["__implicit"] && i+1 >= l) {

        // explicit matching only, permissioning rule
        // for path is only implied by child so we
        // bail

        result_wc = {flags:0, i:0}
      } else {

        // process the next key of the namespace
        //
        result_wc = this._check(
          keys,
          leaf_wc,
          leaf_wc["__"] === undefined ? flags : leaf_wc["__"],
          i+1,
          explicit,
          l
        )
      }
    }

    if(explicit && result.i == 0 && result_wc.i == 0) {
      return {flags: 0, i: i}
    }

    if(result_wc.flags !== undefined) {
      if(result.i < result_wc.i || result.flags === undefined)
        return result_wc
    }

    if(result.flags !== undefined) {
      if(result.i > i || flags === undefined)
        return result
    }

    return {flags:flags, i:i}

  },

  /**
   * Returns the permission flags for the provided
   * namespace
   *
   * @method get_permissions
   * @param {String} namespace
   * @param {Boolean} explicit
   */

  get_permissions : function(namespace, explicit) {
    return this._check(
      this.namespace_keys(namespace),
      this.index,
      undefined,
      0,
      explicit,
      0
    ).flags
  },

  /**
   * Check if the provided namespace is permissioned
   * for the provided permissioning level (flags)
   *
   * @method check
   * @param {String} namesapce
   * @param {Number|String} flags
   * @param {Boolean} explicit
   * @returns {Boolean}
   */

  check : function(namespace, level, explicit) {
    level = this.int_flags(level)
    if(this.expandable(namespace)) {
      var i, _namespace;
      var namespaces = this.expand(namespace, null, null, null, explicit);
      for(i in namespaces) {
        if( (this.get_permissions(namespaces[i], explicit) & level) != 0)
          return true;
      }
      return false;
    }
    return ((this.get_permissions(namespace, explicit) & level) != 0)
  },

  /**
   * Returns whether or not the provided namespaces
   * is expandable.
   *
   * A namespace is expandable if it's path contains `?`
   * keys.
   *
   * @method expandable
   * @param {String} namespace
   * @returns {Boolean}
   */

  expandable : function(namespace) {
    if(!namespace)
      return
    return namespace.search(/\?/) > -1
  },


  /**
   * Returns an array of expanded namespaces for the
   * provided namespace path
   *
   * Any `?` key in the namespace path will be expanded into
   * keys that are in the permission index at that location
   *
   * Example:
   *
   * If your permission rules look like
   *
   * - a.b.c
   * - a.c.c
   *
   * Passing 'a.?.c' to this function will return a list
   * containing both paths
   *
   * @method expand
   * @param {Array|String} keys namespace path
   * @param {Object} index reference current location in the index
   * @param {Array} path path of current location
   * @param {Bool} explicit only return explicit rule matches
   * @param {Bool} exact only return exact length matches
   * @returns {Array}
   */

  expand : function(keys, index, path, length, explicit, exact) {

    if(typeof keys == "string")
      keys = keys.split(".")


    if(!index)
      index = this.index

    if(!path)
      path = []

    if(!length)
      length = keys.length

    var _namespace, _path, k, token = keys[0], result=[]

    for(k in index) {


      if(k.charAt(0) == "_")
        continue

      if(token == k || token == "?" || k == "*") {
        if(k == "*" && token != "?") {
          _path = path.concat([token])
        } else {
          _path = path.concat([k])
        }

        if( (_path.length == length || !exact) && (index[k]["__"] || !explicit)) {
          _namespace = _path.join(this.delimiter).replace(/[\.\*]+$/g,"")
          if(_namespace)
            result.push(_namespace)
        }

        result = result.concat(
          this.expand([].concat(keys).splice(1,keys.length),index[k], _path, length, explicit, exact)
        )

      }

    }

    return result

  },

  /**
   * Takes a namespace string and returns its pieces
   * in an array
   *
   * @method namespace_keys
   * @returns {Array}
   */

  namespace_keys : function(namespace) {
    return namespace.split(this.delimiter)
  },

  /**
   * Update the permissioning index
   *
   * @method update_index
   * @private
   */

  update_index : function() {

    var parent_p, branch, i, namespace, k, p, idx = {}
    var value, keys, key;

    for(namespace in this.rules) {
      branch = idx
      value = this.rules[namespace]
      parent_p = GRAINY_CONST.PERM_DENY
      keys = this.namespace_keys(namespace)
      for(i=0; i<keys.length; i++) {
        key = keys[i];
        if(!branch[key]) {
          branch[key] = {"__": parent_p, "__implicit":true}
        }

        branch = branch[key]
        parent_p = branch["__"]
      }

      branch["__"] = value;
      branch["__implicit"] = false;
    }

    this.index = idx

  },

  /**
   * Take string permission flags and return int
   * permission flags
   *
   * @method int_flags
   * @param {String} flags
   * @returns {Number}
   */

  int_flags : function(flags) {
    var i, int_flag, str_flag, flag, r = 0;

    if(!flags)
      return r

    if(typeof flags == "number")
      return flags

    for(i = 0; i < flags.length; i++) {
      for(int_flag in this.flags) {
        str_flag = this.flags[int_flag]
        if(str_flag == flags.charAt(i))
          r = r | int_flag;
      }
    }

    return r;
  }

}




})();
