class Api::V1::RelevantsController < ApplicationController

  def index
    params.require(:gov)
    params.require(:category)
    @relevants = Relevants.only(:gov, :category, :words, :neighbourhoods).where(category: Integer(params[:category])).where(gov: Integer(params[:gov]))
    render :status => 200, :json => @relevants.limit(20)
  end

  def all
    #@relevants = Relevants.only(:gov, :category, :words, :neighborhood)
    @relevants = Relevants.all
    render :status => 200, :json => @relevants.limit(20)
  end

end
