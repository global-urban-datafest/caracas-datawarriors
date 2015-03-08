class Api::V1::TweetsController < ApplicationController

  def index
    params.require(:gov, :category)
    # TODO: order by relevance
    @tweets = Tweets.only(:id, :text, :created_at, :retweet_count, :sentiment, :gov)
    render :status => 200, :json => @tweets.where(gov: params[:gov]).where(category_id: params[:category]).limit(20)
  end


  def sentiment
    params.require(:gov, :category)
    none = -2
    neg = -1
    neu = 0
    pos = 1

    all = Tweets.only(:id, :text, :created_at, :retweet_count, :sentiment, :gov).where(gov: params[:gov]).where(category_id: params[:category])

    positive = all.where(:sentiment => pos).limit(20)
    negative = all.where(:sentiment => neg).limit(20)
    neutral  = all.any_of({ sentiment: none }, { sentiment: neu}).limit(20)

    @tweets = {negative: negative, neutral: neutral, positive: positive}

    render status: 200, json: @tweets
  end

end