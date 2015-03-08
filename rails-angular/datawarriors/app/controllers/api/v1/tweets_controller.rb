class Api::V1::TweetsController < ApplicationController
  def index
    @tweets = Tweets.first
    render :status => 200, :json => @tweets
  end
end
