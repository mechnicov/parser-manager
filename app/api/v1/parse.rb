module API
  module V1
    class Parse < Grape::API
      version :v1, using: :path

      desc I18n.t('grape.descriptions.api.v1.parse.post')
      params do
        requires :url, type: String
        requires :file, type: File
      end
      post :parse do
        ParseManager.(file: params.dig(:file, :tempfile), url: params[:url])
        { message: I18n.t(:was_parsed, url: params[:url]) }
      end
    end
  end
end
