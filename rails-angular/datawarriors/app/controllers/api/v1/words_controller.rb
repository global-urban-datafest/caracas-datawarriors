class Api::V1::TweetsController < ApplicationController

  def index
    params.require(:category, :gov, :ordering)
    @tweets = Tweets.only(:id, :text, :created_at, :neighborhood, :retweet_count, :gov, :similarity_id, :category_id)
    render :status => 200, :json => @tweets.where(category_id: params[:category]).limit(20)
  end


  def sentiment
    none = -2
    neg = -1
    neu = 0
    pos = 1

    all = Tweets.only(:id, :text, :created_at, :neighborhood, :retweet_count, :gov, :similarity_id, :category_id)

    positive = all.where(:sentiment => pos).limit(20)
    negative = all.where(:sentiment => neg).limit(20)
    neutral  = all.any_of({ sentiment: none }, { sentiment: neu}).limit(20)

    @tweets = {negative: negative, neutral: neutral, positive: positive}

    render status: 200, json: @tweets
  end

end
