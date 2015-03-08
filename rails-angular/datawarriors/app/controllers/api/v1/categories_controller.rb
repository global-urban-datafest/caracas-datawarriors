class Api::V1::CategoriesController < ApplicationController

  def index
    categories = Categories.only(:cat_id, :name)
    @categories = []
    categories.each { |x| @categories << { id: x.cat_id, name: x.name } }
    render :status => 200, :json => @categories
  end

  def all
    @categories = Categories.all
    render :status => 200, :json => @categories
  end

end
