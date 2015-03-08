class Api::V1::CategoriesController < ApplicationController

  def index
    params.require(:gov, :category)
    @categories = Category.only(:id, :name)
    render :status => 200, :json => @categories
  end

end
