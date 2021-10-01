require 'grape'
require 'grape-swagger'

require_relative 'config/application'

module API
  class Root < Grape::API
    format :json
    prefix :api

    mount V1::Parse

    add_swagger_documentation(
      doc_version: '1.0.0',
      info: {
        title: 'Parser manager',
      }
    )
  end
end

Application =
  Rack::Builder.new do
    use Rack::Static,
      root: File.join(__dir__, 'public', 'docs'),
      urls: %w[/css /js /images]

    map '/' do
      run API::Root
    end

    map '/docs' do
      run ->(env) do
        [
          200,
          {},
          File.open(File.join(__dir__, 'public', 'docs', 'index.html'), File::RDONLY)
        ]
      end
    end
  end
