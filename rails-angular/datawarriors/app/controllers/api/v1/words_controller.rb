class Api::V1::WordsController < ApplicationController

  def index
    params.require(:gov)
    params.require(:category)
    @words = Words.only(:gov, :category, :words)
    render :status => 200, :json => @words.where(category: Integer(params[:category])).where(gov: Integer(params[:category])).limit(20)
  end

end
