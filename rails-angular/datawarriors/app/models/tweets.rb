class Tweets
  include Mongoid::Document

  field :id, type: String
  field :text, type: String
  field :gov, type: String
end
