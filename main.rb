require 'grape'

module API
  class Root < Grape::API
    format :json
    prefix :api
  end
end

Application =
  Rack::Builder.new do
    map '/' do
      run API::Root
    end
  end
