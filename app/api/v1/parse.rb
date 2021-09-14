module API
  module V1
    class Parse < Grape::API
      version :v1, using: :path

      helpers do
        def server_error!(message, status)
          error!({ error: message }, status)
        end
      end

      rescue_from :all, ->(e) { server_error!(e.message, 500) }
      rescue_from ParseManager::UnsupportedFileTypeError, ActiveRecord::RecordInvalid,
        ->(e) { server_error!(e.message, 422) }
      rescue_from :grape_exceptions

      desc 'Parse the file'
      params do
        requires :url, type: String
        requires :file, type: File
      end
      post :parse do
        ParseManager.(file: params.dig(:file, :tempfile), url: params[:url])
        { message: "#{params[:url]} was parsed successfully" }
      end
    end
  end
end
