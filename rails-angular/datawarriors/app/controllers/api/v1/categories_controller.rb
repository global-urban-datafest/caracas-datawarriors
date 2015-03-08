class Api::V1::CategoriesController < ApplicationController

  def index
    @categories = Categories.only(:id, :name)
    render :status => 200, :json => @categories
  end

  def all
    @categories = Categories.only(:id, :name)
    render :status => 200, :json => @categories
  end

end
