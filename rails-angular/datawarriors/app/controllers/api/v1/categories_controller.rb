class Api::V1::CategoriesController < ApplicationController

  def index
    params.require(:gov, :category)
    @tweets = Categories.only(:id, :name)
    render :status => 200, :json => @tweets.where(gov: params[:gov]).where(category_id: params[:category]).limit(20)
  end

end
