class Tweets
  include Mongoid::Document

  field :id, type: Integer
  field :text, type: String
  field :created_at, type: DateTime
  field :retweet_count, type: Integer
  field :sentiment, type: Integer
  field :gov, type: String
  #field :similarity_id, type: Integer
  #field :category_id, type: Integer
  #field :neighborhood, type: String
end
