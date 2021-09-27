module Docx
  class Document
    def initialize(path_or_io, options = {})
      @replace = {}

      # if path-or_io is string && does not contain a null byte
      if (path_or_io.instance_of?(String) && !/\u0000/.match?(path_or_io))
        @zip = Zip::File.open(path_or_io)
      else
        @zip = Zip::File.open_buffer(path_or_io)
      end

      document = @zip.glob('word/document*.xml').first
      raise Errno::ENOENT if document.nil?

      @document_xml = document.get_input_stream.read.gsub("<w:tab/>", "<w:t>\t</w:t>")
      @doc = Nokogiri::XML(@document_xml)
      load_styles
      yield(self) if block_given?
    ensure
      @zip.close
    end
  end
end
