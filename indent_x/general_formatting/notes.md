# Document hierarchy

* root [document|collection]

* Document
  * elements : array of type [Property|Comment]

* Collection
  * children : array of type [Value|Comment]

* Property
  * name : PropertyName
  * value : Value

* PropertyName
  * value : string
  * comments : Comment[]

* Value
  * value_type : string
  * value : any
  * _original_value : string
  * comments : Comment[]

Comment
