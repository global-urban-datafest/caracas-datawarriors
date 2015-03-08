class Relevants
  include Mongoid::Document

  field :gov, type: Integer
  field :category, type: Integer
  field :words, type: Hash
  field :neighbourhoods, type: Hash
end
