class Tweets
  include Mongoid::Document

  field :id, type: Integer
  field :text, type: String
  field :created_at, type: String
  field :retweet_count, type: Integer
  field :sentiment, type: Integer
  field :gov, type: Integer
  field :is_base, type: Integer
  field :category, type: Integer
  #field :similarity_id, type: Integer
  #field :neighborhood, type: String
end
