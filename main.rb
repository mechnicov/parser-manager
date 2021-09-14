require 'grape'

require_relative 'config/application'

module API
  class Root < Grape::API
    format :json
    prefix :api

    mount V1::Parse
  end
end

Application =
  Rack::Builder.new do
    map '/' do
      run API::Root
    end
  end
