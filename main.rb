require 'grape'

Dir[File.join(__dir__, 'app', 'lib', '**', '*.rb')].each { |f| require f }
Dir[File.join(__dir__, 'app', 'models', '**', '*.rb')].each { |f| require f }
Dir[File.join(__dir__, 'app', 'api', '**', '*.rb')].each { |f| require f }

DatabaseConnector.establish_connection

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
