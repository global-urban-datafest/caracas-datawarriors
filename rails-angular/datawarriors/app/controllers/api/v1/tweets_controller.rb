class Api::V1::TweetsController < ApplicationController
  def index
    render :status => 200, :json => {:name => "Glebsbia"}
  end
end
