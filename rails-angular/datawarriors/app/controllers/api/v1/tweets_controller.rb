class Api::V1::TweetsController < ApplicationController

  def index
    params.require(:gov)
    params.require(:category)
    # TODO: order by relevance
    @tweets = Tweets.only(:id, :text, :created_at, :retweet_count, :sentiment, :gov, :category).where(is_base: 0)
    render :status => 200, :json => @tweets.where(gov: Integer(params[:gov])).where(category: Integer(params[:category])).limit(20)
  end


  def sentiment
    params.require(:gov)
    params.require(:category)
    none = -2
    neg = -1
    neu = 0
    pos = 1

    all = Tweets.only(:id, :text, :created_at, :retweet_count, :sentiment, :gov, :category).where(is_base: 0).where(gov: Integer(params[:gov])).where(category: Integer(params[:category]))

    positive = all.where(:sentiment => pos).limit(20)
    negative = all.where(:sentiment => neg).limit(20)
    neutral  = all.any_of({ sentiment: none }, { sentiment: neu}).limit(20)

    @tweets = {negative: negative, neutral: neutral, positive: positive}

    render status: 200, json: @tweets
  end


  def all
    @tweets = Tweets.only(:id, :text, :created_at, :retweet_count, :sentiment, :gov).where(is_base: 0)
    render :status => 200, :json => @tweets.limit(20)
  end


  def first
    @tweets = Tweets.where(is_base: 0)
    render :status => 200, :json => @tweets.where(category: 0).limit(10)
  end

end
