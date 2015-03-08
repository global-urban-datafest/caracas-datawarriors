class Words
  include Mongoid::Document

  field :gov, type: Integer
  field :category, type: Integer
  field :words, type: String
end
