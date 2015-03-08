class Categories
  include Mongoid::Document

  field :cat_id, type: Integer
  field :name, type: String
  
end
